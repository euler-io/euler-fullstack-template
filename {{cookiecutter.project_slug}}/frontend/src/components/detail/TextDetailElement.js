import React, { useEffect } from "react";
import axios from "axios";
import create from "zustand";
import qs from "querystring";
import { withStyles } from "@material-ui/core";
import PropTypes from "prop-types";
import { TextDetail } from "euler-search-components";

const styles = (theme) => ({});

const useStore = create((set) => ({
  fragments: [],
  hasMore: true,
  page: 0,
  loadFragments: (id, config, page = 0) => {
    const params = { page };
    const method = config["method"] ? config["method"].toUpperCase() : "GET";
    const url =
      method === "GET"
        ? `${config["url"]}${id}?${qs.stringify(params)}`
        : `${config["url"]}${id}`;
    axios
      .request({
        url: url,
        method: method,
        data: params,
      })
      .then((response) => {
        set((state) => {
          const fragments =
            page > 0
              ? [...state.fragments, ...response.data.hits]
              : [...response.data.hits];
          const total = response.data.total_hits;
          const hasMore = total > fragments.length;
          return {
            fragments,
            hasMore,
            page: state.page + 1,
          };
        });
      })
      .catch((e) => {
        console.info("error", e);
      });
  },
}));

const TextDetailElement = ({ id, config }) => {
  const { fragments, hasMore, page, loadFragments } = useStore();
  useEffect(() => {
    loadFragments(id, config, 0);
  }, [id, loadFragments, config]);
  return (
    <div>
      <TextDetail
        fragments={fragments}
        onLoadMore={() => loadFragments(id, config, page)}
        hasMoreFragments={hasMore}
        fragmentDecode={(f) => ({ id: f.id, text: f.content })}
      />
    </div>
  );
};

TextDetailElement.propTypes = {
  id: PropTypes.string.isRequired,
  config: PropTypes.object.isRequired,
};

TextDetailElement.defaultProps = {};

export default withStyles(styles)(TextDetailElement);
