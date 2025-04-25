import axios from 'axios';

export const getPostgresDatasource = async () => {
  let ds = {
    uid: 'PA942B37CCFAF5A81',
    type: 'postgres'
  };
  let dsid = 1;

  const config = {
    method: 'get',
    url: '/grafana/api/datasources',
    headers: {}
  };

  await axios(config)
    .then(function (response) {
      const tmp = response.data.find((el: { type: string }) => el.type === 'postgres');
      if (tmp !== undefined) {
        ds = { uid: tmp.uid, type: tmp.type };
        dsid = tmp.id;
      }
    })
    .catch(function (error) {
      console.log(error);
    });

  return { ds, dsid };
};
