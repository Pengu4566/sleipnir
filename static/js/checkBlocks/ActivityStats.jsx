import React from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
import Enumerable from "linq";

export default class ActivityStatsBlock extends React.Component {
  render() {
    var data = this.props.name.data;
    // for (var i = 0; i < data.length; i++) {
    //   data[i].count = parseInt(data[i].count);
    // }
    var query = Enumerable.from(data)
      .groupBy(
        "{activityType: $.activityType, project: $.project }",
        "parseInt($.count) | 0",
        "{activityType: $.activityType, project: $.project, count: parseInt($$.sum()) }",
        "$.activityType + ' ' + $.project"
      )
      .toArray();
    for (var i = 0; i < query.length; i++) {
      query[i].index = i + 1;
    }
    const columns = [
      {
        Header: "id",
        accessor: "index",
        id: "index",
        show: false
      },
      {
        Header: "Activity Type",
        accessor: "activityType"
      },
      {
        Header: "Project",
        accessor: "project"
      },
      {
        Header: "Time Used",
        accessor: "count"
      }
    ];
    return (
      <ReactTable
        columns={columns}
        data={query}
        filterable
        defaultFilterMethod={(filter, row) =>
          String(row[filter.id])
            .toLowerCase()
            .includes(filter.value.toLowerCase())
        }
        showFilters={false}
        defaultPageSize={10}
        showPageSizeOptions={false}
        defaultSorted={[
          {
            id: "count",
            desc: true
          },
          {
            id: "project",
            desc: false
          },
          {
            id: "activityType",
            desc: false
          }
        ]}
      />
    );
  }
}
