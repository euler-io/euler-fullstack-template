import React from "react";
import { useParams } from "react-router-dom";

const SearchPage = () => {
  const { id } = useParams();
  return <div>{id}</div>;
};

export default SearchPage;
