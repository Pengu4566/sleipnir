import React from "react";

export default class ImproperNamedVarBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no improperly named variable.</p>
          <p>
            {" "}
            --------------------------------------------------------------------------------------------------------------{" "}
          </p>
        </div>
      );
    } else if (this.props.name == "[There is no variable in your project.]") {
      return (
        <div>
          <p>There is no variable in your project.</p>
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
            A proper variable name should start with an abbreviation of data
            type, following by a hyphen to data name. Variables that are not
            properly named include:{" "}
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
