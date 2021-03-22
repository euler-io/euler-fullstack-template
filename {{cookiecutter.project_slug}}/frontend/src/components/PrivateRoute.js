import React from "react";
import PropTypes from "prop-types";
import AuthService from "./auth";
import { Redirect, Route, useLocation } from "react-router-dom";
import qs from "querystring";

const PrivateRoute = ({ component: Component, auth, children, ...rest }) => {
  const location = useLocation();
  if (auth.isLoggedIn()) {
    return <Component {...rest}>{children}</Component>;
  } else {
    let next = location.pathname;
    if (location.search) {
      next = `${location.pathname}${location.search}`;
    }
    return (
      <Redirect
        to={{
          pathname: auth.params.loginPath,
          search: `?${qs.stringify({ next })}`,
          state: { referrer: next },
        }}
      />
    );
  }
};

PrivateRoute.propTypes = {
  component: PropTypes.node,
  auth: PropTypes.objectOf(AuthService).isRequired,
};

PrivateRoute.defaultProps = {
  component: Route,
};

export default PrivateRoute;
