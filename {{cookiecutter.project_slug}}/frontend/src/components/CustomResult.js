import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { SimpleResult } from "euler-search-components";

const LinkResult = ({ to, children, ...rest }) => {
  return (
    <RouterLink to={to} {...rest}>
      {children}
    </RouterLink>
  );
};

const CustomResult = (props) => {
  return <SimpleResult {...props} linkComponent={LinkResult} />;
};

export default CustomResult;
