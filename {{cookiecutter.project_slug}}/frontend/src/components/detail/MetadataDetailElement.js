import React, { useEffect } from "react";
import axios from "axios";
import create from "zustand";
import qs from "querystring";
import { withStyles } from "@material-ui/core";
import PropTypes from "prop-types";
import { MetadataDetail } from "euler-search-components";

const styles = (theme) => ({});

const decodeMetadata = (m) => {
  return Object.entries(m).map((m) => {
    const name = m[0];
    const value = m[1] ? m[1].toString() : "";
    return { name, value };
  });
};

const useStore = create((set) => ({
  metadata: [],
  loadMetadata: (id, config) => {
    const params = {};
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
        const metadata = decodeMetadata(response.data);
        set((state) => {
          return {
            metadata,
          };
        });
      })
      .catch((e) => {
        console.info("error", e);
      });
  },
}));

const MetadataDetailElement = ({ id, config }) => {
  const { metadata, loadMetadata } = useStore();
  useEffect(() => {
    loadMetadata(id, config);
  }, [id, loadMetadata, config]);
  return (
    <div>
      <MetadataDetail metadata={metadata} />
    </div>
  );
};

MetadataDetailElement.propTypes = {
  id: PropTypes.string.isRequired,
  config: PropTypes.object.isRequired,
};

MetadataDetailElement.defaultProps = {};

export default withStyles(styles)(MetadataDetailElement);
