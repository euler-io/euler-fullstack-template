import React from "react";
import "fontsource-roboto";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import MomentUtils from "@date-io/moment";
import { AppLayout } from "euler-search-components";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import AppMenu from "./AppMenu";
import { SearchPage, LoginPage } from "./pages";
import AuthService from "./components/auth";
import PrivateRoute from "./components/PrivateRoute";

const App = () => {
  const auth = new AuthService();
  return (
    <MuiPickersUtilsProvider utils={MomentUtils}>
      <Router>
        <AppLayout title="Base Project" menu={<AppMenu />}>
          <Switch>
            <Route exact path="/">
              <div>Home</div>
            </Route>
            <Route exact path="/login">
              <LoginPage />
            </Route>
            <PrivateRoute auth={auth} exact path="/search/:id">
              <SearchPage />
            </PrivateRoute>
          </Switch>
        </AppLayout>
      </Router>
    </MuiPickersUtilsProvider>
  );
};

export default App;
