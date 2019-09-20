import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
<link
  rel="stylesheet"
  href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
></link>;

export default class Table1ContentHTML extends React.Component {
  render() {
    if (this.props.name == []) {
      return;
    } else {
      var data = this.props.name;

      const columns = [
        {
          Header: "id",
          accessor: "index",
          id: "index",
          show: false
        },
        {
          Header: "Name",
          accessor: "name"
        },
        {
          Header: "File",
          accessor: "file"
        },
        {
          Header: "Type",
          accessor: "type"
        },
        {
          Header: "Error",
          accessor: "error"
        },
        {
          Header: "Project",
          accessor: "project"
        }
      ];

      return (
        <ReactTable
          className="table table_fixed ml-2 mr-2"
          columns={columns}
          data={this.props.name}
          defaultPageSize={10}
          filterable
          defaultFilterMethod={(filter, row) =>
            String(row[filter.id])
              .toLowerCase()
              .includes(filter.value.toLowerCase())
          }
          showFilters={false}
          showPageSizeOptions={false}
        />
      );
    }
  }
}
