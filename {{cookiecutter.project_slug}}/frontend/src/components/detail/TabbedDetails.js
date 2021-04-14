import React from "react";
import MetadataDetailElement from "./MetadataDetailElement";
import TextDetailElement from "./TextDetailElement";

const DetailsMap = {
  text: TextDetailElement,
  metadata: MetadataDetailElement,
};

const NotFoundDetail = ({ config }) => {
  return <div>The detail screen '{config.type}' has not been created yet.</div>;
};

const TabbedDetails = (detail, mapping = DetailsMap) => {
  const { type } = detail;
  // component does exist
  if (typeof mapping[type] !== "undefined") {
    return mapping[type];
  }
  // component doesn't exist yet
  return NotFoundDetail;
};

export { NotFoundDetail, DetailsMap };
export default TabbedDetails;
