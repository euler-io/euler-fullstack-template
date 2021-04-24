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
    const state = { referrer: next };
    const search = `?${qs.stringify({ next })}`;
    console.info(`User not logged in. Redirecting to ${auth.params.loginURL}.`);
    const to = {
      pathname: auth.params.loginURL,
      search: search,
      state: state,
    };
    return <Redirect to={to} />;
  }
};

PrivateRoute.propTypes = {
  component: PropTypes.elementType,
  auth: PropTypes.instanceOf(AuthService).isRequired,
};

PrivateRoute.defaultProps = {
  component: Route,
};

export default PrivateRoute;
