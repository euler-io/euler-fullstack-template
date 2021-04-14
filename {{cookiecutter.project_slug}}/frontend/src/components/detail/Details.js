import TabbedDetail from "./TabbedDetail";
import TabbedDetails, { DetailsMap as TabbedDetailMap } from "./TabbedDetails";

const DetailsMap = {
  ...TabbedDetailMap,
  tabbed: TabbedDetail,
};

const Details = (detail, mapping = DetailsMap) => {
  return TabbedDetails(detail, mapping);
};

export default Details;
