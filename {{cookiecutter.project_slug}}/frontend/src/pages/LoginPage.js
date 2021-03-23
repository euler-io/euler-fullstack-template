import React from "react";
import {
  Button,
  Dialog,
  DialogContent,
  DialogActions,
  Slide,
  Typography,
} from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";
import create from "zustand";
import { withStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import AuthService from "../components/auth";
import { useHistory, useLocation } from "react-router-dom";
import qs from "querystring";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const useStore = create((set) => ({
  username: "",
  password: "",
  loginError: false,
  update: (newState) => set((state) => ({ ...newState })),
}));

const styles = (theme) => ({
  loginForm: {
    margin: theme.spacing(2),
  },
  alert: {
    margin: theme.spacing(2, 0),
  },
  username: {
    margin: theme.spacing(2, 0),
    width: "100%",
  },
  password: {
    margin: theme.spacing(2, 0),
    width: "100%",
  },
});

const LoginPage = (props) => {
  const { classes, title, auth } = props;
  const { username, password, update, loginError } = useStore();
  const location = useLocation();
  const history = useHistory();

  const getGoto = () => {
    if (location.search) {
      const params = qs.parse(location.search.replace("?", ""));
      if (params.next) {
        return params.next;
      }
    }
    return "/";
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    update({ loginError: false });
    auth.signInWithUsernameAndPassword(username, password).then(
      () => {
        history.push(getGoto());
      },
      (error) => {
        console.error(error);
        update({ loginError: true });
      }
    );
  };
  const handleUpdate = (event) => {
    update({
      [event.target.name]: event.target.value,
    });
  };
  return (
    <div>
      <Dialog
        open={true}
        aria-labelledby="login-title"
        TransitionComponent={Transition}
      >
        <DialogContent>
          <div className={classes.loginForm}>
            <Typography variant="h3">{title}</Typography>
            <ValidatorForm
              method="post"
              onSubmit={handleSubmit}
              onError={(errors) => console.log(errors)}
            >
              {loginError && (
                <Alert
                  className={classes.alert}
                  severity="error"
                  variant="outlined"
                >
                  Invalid username or password.
                </Alert>
              )}
              <div className={classes.username}>
                <TextValidator
                  type="text"
                  name="username"
                  label="Username"
                  value={username}
                  validators={["required"]}
                  errorMessages={["Enter your username."]}
                  onChange={handleUpdate}
                  className={classes.username}
                />
              </div>
              <div className={classes.password}>
                <TextValidator
                  type="password"
                  name="password"
                  label="Password"
                  value={password}
                  validators={["required"]}
                  errorMessages={["Enter your password."]}
                  onChange={handleUpdate}
                  className={classes.password}
                />
              </div>
              <DialogActions>
                <Button variant="contained" color="primary" type="submit">
                  Log in
                </Button>
              </DialogActions>
            </ValidatorForm>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

LoginPage.propTypes = {
  title: PropTypes.string,
  auth: PropTypes.objectOf(AuthService).isRequired,
};

LoginPage.defaultProps = {
  title: "Login",
};

export default withStyles(styles)(LoginPage);
