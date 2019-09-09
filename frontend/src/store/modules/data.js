import api from '../../api'

// initial state
const state = {
    // shape: [{ id, title, genres, viewCnt, rating }]
    movieSearchList: [],
    dialogFlag: false,
    curMovie: "",
    viewUser: [],
    userSearchList: [],
    userMovie: []
}

// actions
const actions = {
    async searchUserMovie({ commit }, params) {
        const resp = await api.searchRating(params)
        const movienames = resp.data
        commit('setUserMovie', movienames)
    },
    async searchUser({ commit }, params) {
        const resp = await api.searchUser(params)
        const users = resp.data.map(d => ({
            userid: d.id,
            username: d.username,
            gender: d.gender,
            age: d.age,
            occupation: d.occupation
        }))
        commit('setUserList', users)
    },
    async searchMovies({ commit }, params) {
        const resp = await api.searchMovies(params)
        if (params["mode"] == 'user') {
            const users = resp.data.map(d => ({
                userid: d.userid
            }))
            commit('setViewUser', users)
        } else if (params["mode"] == 'usermovie') {

        } else {
            const movies = resp.data.map(d => ({
                id: d.id,
                title: d.title,
                genres: d.genres_array,
                viewCnt: d.viewCnt,
                rating: d.rating,
            }))
            commit('setMovieSearchList', movies)
        }
    },
    async searchRating({ commit }, params) {
        const resp = await api.searchRating(params)
        const users = resp.data.map(d => ({
            username: d.username
        }))
        commit('setViewUser', users)
    },
    changeMovieInfo({ commit }, values) {
        const movie = {
            id: values.id,
            title: values.title,
            genres: values.genres,
            viewCnt: values.viewCnt,
            rating: values.rating,
        }
        commit('setMovieInfo', movie)
    },
    changeDialog({ commit }) {
        commit('setDialog')
    },
}

// mutations
const mutations = {
    setUserMovie(state, movienames) {
        state.userMovie = movienames
    },
    setUserList(state, users) {
        state.userSearchList = users.map(m => m)
    },
    setMovieSearchList(state, movies) {
        state.movieSearchList = movies.map(m => m)
    },
    setMovieInfo(state, movie) {
        state.curMovie = movie
    },
    setDialog(state) {
        state.dialogFlag = !state.dialogFlag
    },
    setViewUser(state, user) {
        state.viewUser = user
    },
}

export default {
    namespaced: true,
    state,
    actions,
    mutations
}