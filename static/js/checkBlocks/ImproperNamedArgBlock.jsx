import React from "react";

export default class ImproperNamedArgBlock extends React.Component {
  render() {
    if (this.props.name == "[]") {
      return (
        <div>
          <p>There is no improperly named argument.</p>
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
            A proper argument name should starts 'in_', 'out_', or 'io_' to
            annotate the argument's property. Arguments that are not properly
            named include:{" "}
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
