import React from "react";

export default class NotAnnotWfBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no workflow that is invoked but not annotated.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else if (this.props.name == "The file you uploaded is not completed.") {
      return (
        <div>
          <p>
            An invoked workflow should always be annotated. However, the file
            you uploaded is not completed, so we cannot analyze workflow
            annotation for you.
          </p>
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
            An invoked workflow should always be annotated. Workflows that are
            invoked but are not annotated include:{" "}
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
