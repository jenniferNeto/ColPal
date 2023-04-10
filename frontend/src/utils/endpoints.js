

export const get_user_pipelines = (id) => ({
    url: `/pipelines/user/${id}/`,
    method: 'get',
    headers: {},
    isAuth: true,
})
export const post_pipeline_file = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/upload/`,
    method: 'post',
    headers: {'Content-Type': 'multipart/form-data'},
    isAuth: true,
})

export const get_pipeline_due_date = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/due/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const get_pipeline_uploads = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/files/`,
    method: 'get',
    headers: {},
    isAuth: true,
})
export const get_all_users = () => ({
    url: `/users/`,
    method: 'get',
    headers: {},
    isAuth: false,
})

