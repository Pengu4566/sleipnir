import React from "react";

export default class UnusedArgBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no unused argument.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else if (this.props.name == "[There is no argument in your project.]") {
      return (
        <div>
          <p>There is no argument in your project.</p>
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
            An unused argument should be deleted. Arguments that are declared
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
