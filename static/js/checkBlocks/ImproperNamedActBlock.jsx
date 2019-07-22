import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class ImproperNamedActBlock extends React.Component {
  render() {
    if (this.props.name.data == []) {
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>
              Activity naming is evaluated based on the activity type. No
              activity should be named with its default name.
            </p>
            <p>There is no improperly named activity.</p>
          </div>
        </div>
      );
    } else if (
      this.props.name.data == "[There is no activity in your project.]"
    ) {
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>There is no activity in your project.</p>
          </div>
        </div>
      );
    } else if (this.props.name.data == "[Not evaluated]") {
      return <div />;
    } else {
      const columns = [
        {
          Header: "Activity ID",
          accessor: "index"
        },
        {
          Header: "Activity Name",
          accessor: "activityName"
        },
        {
          Header: "From File",
          accessor: "filePath"
        }
      ];
      return (
        <div className="single_check">
          <h3>Activity Naming</h3>
          <div className="check_explain">
            <p>
              Activity naming is evaluated based on the activity type. No
              activity should be named with its default name. Activities that
              are not properly named include:
            </p>
            <ReactTable columns={columns} data={this.props.name.data} />
          </div>
        </div>
      );
    }
  }
}
