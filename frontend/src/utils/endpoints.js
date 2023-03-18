

export const get_user_pipelines = (id) => ({
    url: `/pipelines/user/${id}/`,
    method: 'get',
    isAuth: true,
})

export const get_all_users = () => ({
    url: `/users/`,
    method: 'get',
    isAuth: false,
})

