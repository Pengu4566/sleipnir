import React from "react";

export default class UnusedVarBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no unused variable.</p>
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
            An unused variable should be deleted. Variables that are declared
            but not used include:{" "}
          </p>
          <p> {this.props.name} </p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    }
  }
}
