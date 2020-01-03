import React from "react";
import styles from "../scss/result_header.scss";
import classnames from "classnames";

export default class ResultHeader extends React.Component {
  constructor(props) {
    super(props);
    this.logout = this.logout.bind(this);
  }
  logout() {
    window.location = "/logout";
  }
  render() {
    return (
      <div
        className={classnames(
          "d-flex",
          "justify-cotent-between",
          "algin-self-center",
          styles["header"]
        )}
      >
        <span className={classnames("ml-4", styles["header_text"])}>
          Please review your results
        </span>
        <span
          className={classnames(
            "mr-4",
            styles["header_text"],
            styles["username-cust"]
          )}
        >
          {username}&ensp;
          <i
            className={classnames("fa fa-sign-out", styles["logout-cust"])}
            onClick={() => this.logout()}
          ></i>
        </span>
      </div>
    );
  }
}
