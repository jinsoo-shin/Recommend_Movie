import axios from 'axios'

const apiUrl = '/api'

export default {
    searchMovies(params) {
        return axios.get(`${apiUrl}/movies/`, {
            params,
        })
    },
    searchRating(params) {
        return axios.get(`${apiUrl}/ratings/`, {
            params,
        })
    },
    searchUser(params) {
        return axios.get(`${apiUrl}/auth/signup-many/`, {
            params,
        })
    },
}