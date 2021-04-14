import React, { useEffect } from "react";
import { useParams, useHistory, useLocation } from "react-router-dom";
import axios from "axios";
import create from "zustand";
import {
  Search,
  QueryState,
  useParametersEffect,
} from "euler-search-components";
import qs from "querystring";
import appConfig from "../appConfig";
import Results from "../components/Results";
import mustache from "mustache";
import dompurify from "dompurify";

const useStore = create((set) => ({
  config: null,
  loadConfig: async (id) => {
    return axios
      .get(`/config/${id}`)
      .then((response) => {
        const config = response.data;
        set((state) => ({
          config,
        }));
      })
      .catch((error) => {
        console.error(error);
      });
  },
  update: (newState) => set((state) => ({ ...newState })),
  results: null,
  loading: false,
  total: null,
  query: null,
  took: null,
  previousParameters: null,
  setResultsUndefined: () => {
    set((state) => ({
      results: null,
      loading: false,
      total: null,
      query: null,
      took: null,
      previousParameters: null,
    }));
  },
  search: (parameters, config) => {
    const defaultValues = config["default-values"]
      ? config["default-values"]
      : {};
    const params = { ...defaultValues, ...parameters };

    const method = config["method"] ? config["method"].toUpperCase() : "GET";
    const url =
      method === "GET"
        ? `${config["url"]}?${qs.stringify(params)}`
        : config["url"];

    set((state) => ({
      loading: true,
      previousParameters: params,
    }));

    axios
      .request({
        url: url,
        method: method,
        data: params,
      })
      .then((response) => {
        const results = response.data.hits;
        const total = response.data.total_hits;
        const took = response.data.took;
        const query = getQuery(parameters, config);
        set((state) => ({
          loading: false,
          results,
          total,
          query,
          took,
        }));
      })
      .catch((e) => {
        console.info("error", e);
        set((state) => ({
          loading: false,
          results: null,
          total: null,
          query: null,
          took: null,
        }));
      });
  },
}));

const isMandatoryFieldsPresent = (parameters, config) => {
  if (config["mandatory-fields"] !== undefined) {
    return config["mandatory-fields"]
      .map((f) => parameters[f])
      .reduce((current, p) => current && p && p !== "", true);
  } else {
    return true;
  }
};

const getQuery = (parameters, config) => {
  const searchField = config["search-field"];
  const fields = config["fields"];
  if (searchField !== undefined) {
    return parameters[searchField];
  } else if (fields !== undefined && fields.length > 0) {
    return parameters[fields[0]];
  } else {
    return undefined;
  }
};

const getDefaultValue = (config, field, df = null) => {
  if (
    config &&
    config.config["default-values"] &&
    config.config["default-values"][field]
  ) {
    return config.config["default-values"][field];
  } else {
    return df;
  }
};

const escape = (v) => {
  return dompurify.sanitize(v, { ALLOWED_TAGS: ["em"] });
};

const MUSTACHE_CONFIG = {
  escape: escape,
};

const decodeItem = (item, searchId, config) => {
  const results = config.config["results"];
  const decoded = {};

  const view = {
    ...item,
    baseURL: appConfig.baseURL,
    searchId,
  };

  Object.keys(results).forEach((k) => {
    const value = mustache.render(results[k], view, "", MUSTACHE_CONFIG);
    decoded[k] = value;
  });

  return decoded;
};

const SearchPage = () => {
  const { searchId } = useParams();
  const {
    loadConfig,
    config,
    results,
    total,
    query,
    took,
    loading,
    search,
    setResultsUndefined,
  } = useStore();
  const location = useLocation();
  const history = useHistory();
  const queryState = new QueryState(history, location);
  const parameters = queryState.getParameters();

  const title = config ? config.title : "";
  const filters = config ? config.config.filters : [];
  useEffect(() => loadConfig(searchId), [searchId, loadConfig]);

  useParametersEffect(
    () => {
      if (config && isMandatoryFieldsPresent(parameters, config.config)) {
        search(parameters, config.config);
      } else {
        setResultsUndefined();
      }
    },
    parameters,
    config !== null ? config.config.fields : [],
    true
  );

  const handleParametersChanged = (newParameters) => {
    const resetPage = !("page" in newParameters);
    if (resetPage) {
      const defaultPage = getDefaultValue(config, "page", 0);
      newParameters = {
        ...newParameters,
        page: defaultPage,
      };
    }
    queryState.updateQuery({ ...newParameters });
  };
  return (
    <div>
      <Search
        title={title}
        filters={filters}
        results={results}
        total={total}
        took={took}
        query={query}
        loading={loading}
        parameters={parameters}
        onParametersChanged={handleParametersChanged}
        resultComponents={Results}
        decodeItem={(i) => decodeItem(i, searchId, config)}
      />
    </div>
  );
};

export default SearchPage;
