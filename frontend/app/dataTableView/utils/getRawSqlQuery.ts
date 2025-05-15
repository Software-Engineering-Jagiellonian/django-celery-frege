import { rowLimit } from '../DataTableView';

export const getRawSqlQuery = (page: number, languages: string[], analyzed: number) => {
  let result = `SELECT * FROM repositories_repositoryfile`;

  if (analyzed !== 0) result += ` WHERE analyzed=${analyzed === 1 ? 'true' : 'false'}`;

  if (languages.length > 0) {
    if (analyzed !== 0) result += ` AND `;
    else result += ` WHERE `;
    result += `language IN (`;

    for (let i = 0; i < languages.length - 1; i++) {
      result += `'${languages[i]}', `;
    }
    result += `'${languages[languages.length - 1]}'`;

    result += `)`;
  }

  result += ` ORDER BY id LIMIT ${rowLimit} OFFSET ${page * rowLimit}`;
  return result;
};
