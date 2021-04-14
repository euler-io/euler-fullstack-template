import React from "react";
import CustomResult from "./CustomResult";

const ResultsMap = {
  simple: CustomResult,
};

const NotFoundResult = ({ type }) => {
  return <div>The result {type} has not been created yet.</div>;
};

const Results = (result) => {
  const { type } = result;
  if (type === undefined) {
    // type not defined
    return NotFoundResult;
  } else if (typeof ResultsMap[type] !== "undefined") {
    // component does exist
    return ResultsMap[type];
  } else {
    // component doesn't exist yet
    return NotFoundResult;
  }
};

export default Results;
