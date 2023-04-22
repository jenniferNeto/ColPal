

export const get_user_pipelines = (id) => ({
    url: `/pipelines/user/${id}/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const get_unapproved_pipelines = () => ({
    url: `/pipelines/not-approved/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const get_pipeline_constraints = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/constraints/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const add_pipeline_role = (pipeline_id, role) => ({
    url: `/pipelines/${pipeline_id}/positions/${role}/add/`,
    method: 'post',
    headers: {},
    isAuth: true,
})

export const get_pipeline_roles = (pipeline_id, role) => ({
    url: `/pipelines/${pipeline_id}/positions/${role}/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const delete_pipeline_roles = (pipeline_id, role) => ({
    url: `/pipelines/${pipeline_id}/positions/${role}/delete/`,
    method: 'put',
    headers: {},
    isAuth: true,
})

export const put_approve_pipeline = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/status/`,
    method: 'put',
    headers: {},
    isAuth: true,
})
export const post_pipeline_file = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/upload/`,
    method: 'post',
    headers: {'Content-Type': 'multipart/form-data'},
    isAuth: true,
})

export const post_pipeline_create = () => ({
    url: `/pipelines/create/`,
    method: 'post',
    headers: {'Content-Type': 'application/json'},
    isAuth: true,
})

export const get_pipeline_deadline = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/deadline/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const post_create_constraints = () => ({
    url: `/pipelines/upload/template/`,
    method: 'post',
    headers: {'Content-Type': 'multipart/form-data'},
    isAuth: true,
})

export const get_pipeline_uploads = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/files/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const get_validate_upload = (pipeline_id, file_id) => ({
    url: `/pipelines/${pipeline_id}/files/${file_id}/validate/`,
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

export const get_pipeline_notifications = (pipeline_id) => ({
    url: `/pipelines/${pipeline_id}/notifications/`,
    method: 'get',
    headers: {},
    isAuth: true,
})

export const get_user_notifications = (id) => ({
    url: `/pipelines/user/${id}/notifications/`,
    method: 'get',
    headers: {},
    isAuth: true,
})


