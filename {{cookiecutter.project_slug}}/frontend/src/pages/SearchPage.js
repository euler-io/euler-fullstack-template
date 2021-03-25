import React, { useEffect } from "react";
import { useParams, useHistory, useLocation } from "react-router-dom";
import axios from "axios";
import create from "zustand";
import { Search, QueryState } from "euler-search-components";
import qs from "querystring";

const useStore = create((set) => ({
  config: null,
  loadConfig: async (id) => {
    return axios
      .get(`/config?id=${id}`)
      .then((response) => {
        if (response.data.total_hits === 1) {
          const config = response.data.hits[0].source;
          set((state) => ({
            config,
          }));
        } else {
          set((state) => ({
            config: null,
          }));
        }
      })
      .catch((error) => {
        console.error(error);
      });
  },
  update: (newState) => set((state) => ({ ...newState })),
  results: null,
  loading: false,
  total: null,
  took: null,
  query: null,
  setResultsUndefined: () => {
    set((state) => ({
      results: null,
      loading: false,
      total: null,
      took: null,
      query: null,
    }));
  },
  search: (parameters, config) => {
    const defaultValues = config["default-values"]
      ? config["default-values"]
      : {};
    const method = config["method"] ? config["method"].toUpperCase() : "GET";
    const params = { ...defaultValues, ...parameters };
    const url =
      method === "GET"
        ? `${config["url"]}?${qs.stringify(params)}`
        : config["url"];

    set((state) => ({
      loading: true,
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
        set((state) => ({
          loading: false,
          results,
          total,
          took,
          query: "?",
        }));
      })
      .catch((e) => {
        console.info("error", e);
        set((state) => ({
          loading: false,
          results: null,
          total: null,
          took: null,
          query: null,
        }));
      });
  },
}));

const useParametersEffect = (fn, parameters, arr, asString = false) => {
  let effectArr = arr.map((p) => {
    const v = parameters[p];
    if (Array.isArray(v)) {
      return v.join(",");
    } else if (v === null || v === undefined) {
      return "";
    } else {
      return v;
    }
  });
  if (asString) {
    effectArr = [effectArr.reduce((s, p) => `${s},${p}`, "")];
  }

  useEffect(fn, effectArr);
};

const isMandatoryFieldsPresent = (parameters, config) => {
  if (config !== null && config["mandatory-fields"] !== undefined) {
    return config["mandatory-fields"]
      .map((f) => parameters[f])
      .reduce((current, p) => current && p && p !== "", true);
  } else {
    return true;
  }
};

const SearchPage = () => {
  const { id } = useParams();
  const {
    loadConfig,
    config,
    results,
    setResultsUndefined,
    total,
    took,
    query,
    loading,
    search,
  } = useStore();
  const location = useLocation();
  const history = useHistory();
  const queryState = new QueryState(history, location);
  const parameters = queryState.getParameters();
  useEffect(() => loadConfig(id), [id, loadConfig]);

  useParametersEffect(
    () => {
      if (config && isMandatoryFieldsPresent(parameters, config)) {
        search(parameters, config);
      }
    },
    parameters,
    config !== null ? config.fields : [],
    true
  );

  const handleParametersChanged = (newParameters) => {
    queryState.updateQuery({ ...newParameters });
  };

  return (
    <div>
      {config && (
        <Search
          {...config}
          results={results}
          total={total}
          took={took}
          query={query}
          loading={loading}
          parameters={parameters}
          onParametersChanged={handleParametersChanged}
        />
      )}
    </div>
  );
};

export default SearchPage;
