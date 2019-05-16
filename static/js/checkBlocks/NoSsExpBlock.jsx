import React from "react";

export default class NoSsExpBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no exception that is not handled by screenshot.</p>
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
            An exception should always be recorded by a screenshot activity.
            Exceptions that are not handled by screenshot include:{" "}
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
