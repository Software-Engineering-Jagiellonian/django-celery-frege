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

  await axios({method: 'GET', url: 'http://localhost:3000/api/user', headers: {}}).then(
    (response) => {
      console.log(response.data)
    }
  ).catch((error) => {
    console.log(error)
  })

  await axios(config)
    .then(function (response) {
      const tmp = response.data.find((el: { type: string }) => el.type === 'postgres');
      if (tmp !== undefined) {
        ds = { uid: tmp.uid, type: tmp.type };
        dsid = tmp.id;
      }
    })
    .catch(function (error) {
      if (axios.isAxiosError(error)) {
        console.log("AxiosError:", {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data
        });
      } else {
        console.log(error);
      }
    });

  return { ds, dsid };
};
