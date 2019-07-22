import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class ImproperNamedArgBlock extends React.Component {
  render() {
    if (this.props.name.data == []) {
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>
              Argument naming is evaluated according to argument type, data
              type, and camel case rule.
            </p>
            <p>There is no improperly named argument.</p>
          </div>
        </div>
      );
    } else if (
      this.props.name.data == ["There is no argument in your project."]
    ) {
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>There is no argument in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == ["Not evaluated"]) {
      return <div />;
    } else {
      const columns = [
        {
          Header: "Argument ID",
          accessor: "index"
        },
        {
          Header: "Argument Name",
          accessor: "argumentName"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="single_check">
          <h3>Argument Naming</h3>
          <div className="check_explain">
            <p>
              Argument naming is evaluated according to argument type, data
              type, and camel case rule. Arguments that are not properly named
              include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
