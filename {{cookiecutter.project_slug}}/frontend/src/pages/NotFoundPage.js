import React from "react";
import { Typography } from "@material-ui/core";
import { useLocation } from "react-router-dom";
import { withStyles } from "@material-ui/core/styles";

const styles = (theme) => ({
  notFound: {
    textAlign: "center",
  },
});

const NotFoundPage = ({ classes }) => {
  const location = useLocation();
  return (
    <div className={classes.notFound}>
      <Typography variant="h2">404</Typography>
      <Typography variant="h4">{location.pathname} not found.</Typography>
    </div>
  );
};

export default withStyles(styles)(NotFoundPage);
