import axios from 'axios';
import { rowLimit } from '../DataTableView';
import { getPostgresDatasource } from './getPostgresDatasource';
import { getRawSqlQuery } from './getRawSqlQuery';
import { RepositoryFileItem } from './RepositoryFileItem';

export const getRepoMetrics = async (
  page: number,
  languages: string[],
  analyzed: number
): Promise<RepositoryFileItem[]> => {
  const logsData: RepositoryFileItem[] = [];

  const postgresDatasource = await getPostgresDatasource();

  const data = JSON.stringify({
    queries: [
      {
        refId: 'resp1',
        datasource: postgresDatasource.ds,
        rawSql: getRawSqlQuery(page, languages, analyzed),
        format: 'table',
        datasourceId: postgresDatasource.dsid,
        intervalMs: 0,
        maxDataPoints: 0
      }
    ]
  });

  const config = {
    method: 'post',
    url: '/grafana/api/ds/query',
    headers: {
      'Content-Type': 'application/json'
    },
    data: data
  };

  await axios(config)
    .then(function (response) {
      const resp = response.data.results.resp1.frames[0].data.values;
      for (let i = 0; i < resp[0].length; i++) {
        logsData.push({
          id: resp[0][i],
          analyzed: resp[1][i],
          language: resp[2][i],
          repo_relative_file_path: resp[3][i],
          metrics: resp[4][i],
          analyzed_time: resp[5][i],
          repository_id: resp[6][i]
        });
      }
    })
    .catch(function (error) {
      console.log(error);
    });

  return logsData;
};
