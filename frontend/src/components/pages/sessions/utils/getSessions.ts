import axios from "axios";
import { SessionI } from "../Sessions";

export const getSessions = async () => {
    let result: Array<SessionI>
    result = []

    const config = {
        method: 'get',
        url: `grafana/api/user/auth-tokens`,
        headers: { }
    };
      
    await axios(config)
    .then(function (response) {
        result = response.data
    })
    .catch(function (error) {
        throw Error(error)
    });

    return result
}