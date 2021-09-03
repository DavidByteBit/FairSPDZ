import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import Login from './Login'
import Content from './Content'


export default function Layout(props){
  return(
    <Router>
      <Switch>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/content">
            <Content />
          </Route>
          <Route path="/">
            <Login />
          </Route>
        </Switch>
    </Router>
  )
}