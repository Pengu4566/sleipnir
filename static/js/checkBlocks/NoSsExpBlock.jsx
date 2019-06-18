import React from "react";

export default class NoSsExpBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Try Catch Screenshot</h3>
          <div className="check_explain">
            <p>
              Try catch screenshot is evaluated by checking if all exceptions
              are handled by screenshot.
            </p>
            <p>There is no exception that is not handled by screenshot.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[There is no catch in your project.]") {
      return (
        <div className="single_check">
          <h3>Try Catch Screenshot</h3>
          <div className="check_explain">
            <p>There is no catch in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[Not evaluated]") {
      return <div />;
    } else {
      return (
        <div className="single_check">
          <h3>Try Catch Screenshot</h3>
          <div className="check_explain">
            <p>
              Try catch screenshot is evaluated by checking if all exceptions
              are handled by screenshot. An exception should always be recorded
              by a screenshot activity. Exceptions that are not handled by
              screenshot include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
