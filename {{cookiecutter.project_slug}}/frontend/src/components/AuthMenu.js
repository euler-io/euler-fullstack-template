import React, { useEffect } from "react";
import PropTypes from "prop-types";
import AuthService from "./auth";
import { IconButton, Menu, MenuItem, Link } from "@material-ui/core";
import AccountCircle from "@material-ui/icons/AccountCircle";
import { useHistory, Link as RouterLink } from "react-router-dom";
import create from "zustand";

const useStore = create((set) => ({
  anchorEl: null,
  setAnchorEl: (el) => {
    set((state) => {
      return {
        anchorEl: el,
      };
    });
  },
  loggedIn: false,
  setLoggedIn: (l) => {
    set((state) => {
      return {
        loggedIn: l,
      };
    });
  },
}));

const anchor = {
  vertical: "top",
  horizontal: "right",
};

const AuthMenu = ({ auth, next, login }) => {
  const { anchorEl, setAnchorEl, loggedIn, setLoggedIn } = useStore();
  const open = Boolean(anchorEl);

  const history = useHistory();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleLogout = () => {
    auth.setSession(null);
    setAnchorEl(null);
    history.push(next);
  };

  const onSessionChanged = () => {
    setLoggedIn(auth.isLoggedIn());
  };

  useEffect(() => {
    setLoggedIn(auth.isLoggedIn());
  }, [auth, setLoggedIn]);

  useEffect(() => {
    auth.addSessionListener(onSessionChanged);
    return () => {
      auth.removeSessionListener(onSessionChanged);
    };
  }, [auth, onSessionChanged]);

  return (
    <div>
      {loggedIn ? (
        <>
          <IconButton
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={anchor}
            keepMounted
            transformOrigin={anchor}
            open={open}
            onClose={handleClose}
          >
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </>
      ) : (
        <RouterLink color="inherit" to={login} component={Link}>
          Login
        </RouterLink>
      )}
    </div>
  );
};

AuthMenu.propTypes = {
  auth: PropTypes.instanceOf(AuthService).isRequired,
  next: PropTypes.string,
  login: PropTypes.string,
};

AuthMenu.defaultProps = {
  next: "/",
  login: "/login",
};

export default AuthMenu;
