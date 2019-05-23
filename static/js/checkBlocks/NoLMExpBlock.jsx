import React from "react";

export default class NoLMExpBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no exception that is not handled by log message.</p>{" "}
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else if (this.props.name == "[There is no catch in your project.]") {
      return (
        <div>
          <p>There is no catch in your project.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <p>
            {" "}
            An exception should always be logged. Exceptions that are not logged
            include:{" "}
          </p>
          <p>{this.props.name}</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    }
  }
}
