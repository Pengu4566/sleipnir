import React from "react";

export default class NoLMExpBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div className="single_check">
          <h3>Try Catch Logging</h3>
          <div className="check_explain">
            <p>
              Try catch logging is evaluated by checking if all exceptions are
              handled by log messages.
            </p>
            <p>There is no exception that is not handled by log message.</p>
          </div>
        </div>
      );
    } else if (this.props.name == "[There is no catch in your project.]") {
      return (
        <div className="single_check">
          <h3>Try Catch Logging</h3>
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
          <h3>Try Catch Logging</h3>
          <div className="check_explain">
            <p>
              Try catch logging is evaluated by checking if all exceptions are
              handled by log messages. An exception should always be logged.
              Exceptions that are not logged include:
            </p>
            <p>{this.props.name}</p>
          </div>
        </div>
      );
    }
  }
}
