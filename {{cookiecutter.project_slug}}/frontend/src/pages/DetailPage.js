import React, { useEffect } from "react";
import { Breadcrumbs, makeStyles, Typography } from "@material-ui/core";
import { useParams } from "react-router-dom";
import axios from "axios";
import create from "zustand";
import Details from "../components/detail/Details";
import qs from "querystring";

const useStyles = makeStyles((theme) => ({
  title: {
    margin: theme.spacing(2, 0),
  },
}));

const useStore = create((set) => ({
  title: null,
  config: null,
  loadConfig: async (id) => {
    return axios
      .get(`/detail/${id}`)
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
  loadMetadata: (id, config) => {
    set((state) => {
      return {
        title: null,
      };
    });
    const titleProperty = config["title-property"];
    const params = { source: [titleProperty] };
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
        const metadata = response.data;
        const title = metadata[titleProperty];
        set((state) => {
          return {
            title,
          };
        });
      })
      .catch((e) => {
        console.info("error", e);
      });
  },
}));

const DetailPage = () => {
  const { detailId, id } = useParams();
  const classes = useStyles();
  const { config, loadConfig, title, loadMetadata } = useStore();
  useEffect(() => loadConfig(detailId), [detailId, loadConfig]);
  useEffect(() => {
    if (config !== null) {
      loadMetadata(id, config.config);
    }
  }, [id, loadMetadata, config]);
  const DetailComponent = config !== null ? Details(config) : null;
  return (
    <div>
      <Breadcrumbs aria-label="breadcrumb" className={classes.title}>
        <Typography variant="h4">{title}</Typography>
      </Breadcrumbs>
      {DetailComponent && <DetailComponent id={id} config={config.config} />}
    </div>
  );
};

export default DetailPage;
