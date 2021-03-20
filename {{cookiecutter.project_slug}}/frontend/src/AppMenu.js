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
      <ListItemLink button to="/archiveorg">
        <ListItemIcon>
          <SearchIcon />
        </ListItemIcon>
        <ListItemText primary="Archive.org Search" />
      </ListItemLink>
    </List>
  );
};

export default AppMenu;
