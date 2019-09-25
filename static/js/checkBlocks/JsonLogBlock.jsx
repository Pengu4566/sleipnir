import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";

export default class JsonLogBlock extends React.Component {
  render() {
    var data = JSON.parse(this.props.name.replace(/'/g, '"')).data;
    const columns = [
      {
        Header: "Project ID",
        accessor: "index",
        id: "index",
        show: false
      },
      {
        Header: "Project Name",
        accessor: "projectName"
      },
      {
        Header: "Project Description",
        accessor: "projectDetail.projectDescription"
      },
      {
        Header: "Template",
        accessor: "templateComment"
      }
    ];

    let pgSize = data.length;

    return (
      <ReactTable
        columns={columns}
        data={data}
        defaultPageSize={pgSize}
        showPageSizeOptions={false}
        showPagination={false}
      />
    );
  }
}
