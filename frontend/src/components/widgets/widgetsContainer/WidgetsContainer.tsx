import React, {useEffect, useState} from 'react';
import {useParams} from "react-router-dom";
import {WidgetsHub} from "../hub/WidgetsHub";
import axios from "axios";
import {WidgetRetrieveData} from "../hub/hubTypes";

function WidgetsContainer() {
    const { dashboardId } = useParams();
    const [widgets, setWidgets] = useState<WidgetRetrieveData[]>([])
    const [dashboardName, setDashboardName] = useState('')

    useEffect(() => {
        axios.get(`api/dashboards/uid/${dashboardId}`)
            .then(response => {
                const widgetsTemp: WidgetRetrieveData[] = response.data.dashboard.panels.map((panel: { id: string; title: string; }) => {
                    return (
                        {
                            dashboardId: `${dashboardId}`,
                            widgetId: `${panel.id}`,
                            dashboardName: response.data.dashboard.title,
                            widgetName: panel.title
                        } as WidgetRetrieveData
                    )
                })

                setDashboardName(response.data.dashboard.title)
                setWidgets(widgetsTemp)
            })
    }, [dashboardId])

    return (
      <div>
          <h1 className="text-center">{dashboardName}</h1>
          <WidgetsHub
              widgets= {widgets}
              hubId={`${dashboardId}`}
          />
      </div>
    );
}

export default WidgetsContainer;