import Vue from 'vue'
import VueRouter from 'vue-router'
import EmptyPage from '../components/pages/EmptyPage'
import MovieSearchPage from '../components/pages/MovieSearchPage'
import MostViewPage from '../components/pages/MostViewPage'
import UserSearchPage from '../components/pages/UserSearchPage'
import AdminPage from '../components/pages/AdminPage'
import LoginPage from '../components/pages/LoginPage'
import MyPage from '../components/pages/MyPage'
import TutorialPage from '../components/pages/TutorialPage'

Vue.use(VueRouter)


const router = new VueRouter({
    mode: 'history',
    routes: [
        { path: '/', component: EmptyPage, name: 'home' },
        { path: '/movies/search', component: MovieSearchPage, name: 'movie-search' },
        { path: '/movies/mostviewsearch', component: MostViewPage, name: 'mostview-search' },
        { path: '/movies/user', component: UserSearchPage, name: 'user-search' },
        { path: '/admin', component: AdminPage, name: 'Admin' },
        { path: '/login', component: LoginPage, name: 'Login' },
        { path: '/MyPage', component: MyPage, name: 'MyPage'},
        { path: '/Tutorial', component: TutorialPage, name: 'Tutorial'}
    ],
    scrollBehavior() {
        return { x: 0, y: 0 }
    },
})

export default router