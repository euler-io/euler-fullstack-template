import React from "react";
import { List, ListItem, ListItemIcon, ListItemText } from "@material-ui/core";
import { Link } from "react-router-dom";
import SearchIcon from "@material-ui/icons/Search";

const ListItemLink = (props) => {
  return <ListItem component={Link} {...props} />;
};

const AppMenu = (props) => {
  return (
    <List>
      <ListItemLink button to="/search/sample">
        <ListItemIcon>
          <SearchIcon />
        </ListItemIcon>
        <ListItemText primary="Search Sample" />
      </ListItemLink>
    </List>
  );
};

export default AppMenu;
