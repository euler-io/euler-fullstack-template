import React, { memo } from "react";
import { Paper, Tabs, Tab, makeStyles } from "@material-ui/core";
import PropTypes from "prop-types";
import { useHistory, useLocation, Link } from "react-router-dom";
import { QueryState } from "euler-search-components";
import TabbedDetails from "./TabbedDetails";
import qs from "querystring";

const useStyles = makeStyles({
  root: {
    flexGrow: 1,
  },
});

const TabBody = memo(({ id, tab, detailComponents }) => {
  const DetailComponent = detailComponents(tab);
  const config = tab.config ? tab.config : {};
  return <DetailComponent id={id} config={config} />;
});

function LinkTab({ value, parameters, path, ...rest }) {
  const to = `${path}?${qs.stringify({
    ...parameters,
    tab: value,
  })}`;
  return (
    <Tab
      value={value}
      to={to}
      component={Link}
      onClick={(event) => {
        event.preventDefault();
      }}
      {...rest}
    />
  );
}

const TabbedDetail = ({ id, config, detailComponents }) => {
  const classes = useStyles();

  const location = useLocation();
  const history = useHistory();
  const queryState = new QueryState(history, location);
  const parameters = queryState.getParameters();
  const { tab } = {
    tab: config.tabs[0].id,
    ...parameters,
  };

  const handleChange = (event, newTab) => {
    queryState.updateQuery({ tab: newTab });
  };

  return (
    <div>
      <Paper className={classes.root}>
        <Tabs
          value={tab}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          centered
        >
          {config.tabs.map((t) => (
            <LinkTab
              key={t.id}
              value={t.id}
              parameters={parameters}
              path={location.pathname}
              label={t.title}
            />
          ))}
        </Tabs>
      </Paper>
      {config.tabs.map((t) => (
        <div key={t.id}>
          {t.id === tab ? (
            <TabBody id={id} tab={t} detailComponents={detailComponents} />
          ) : (
            <></>
          )}
        </div>
      ))}
    </div>
  );
};

TabbedDetail.propTypes = {
  id: PropTypes.string.isRequired,
  detailComponents: PropTypes.func,
  config: PropTypes.object.isRequired,
};

TabbedDetail.defaultProps = {
  detailComponents: TabbedDetails,
};

export default TabbedDetail;
