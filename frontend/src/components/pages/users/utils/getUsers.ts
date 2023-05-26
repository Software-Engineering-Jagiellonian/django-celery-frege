import axios from "axios";
import { UserI } from "../Users";

export const getUsers = async (page: number) => {
    let result: Array<UserI>
    result = []

    const config = {
        method: 'get',
        url: `grafana/api/users?perpage=10&page=${page}`,
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