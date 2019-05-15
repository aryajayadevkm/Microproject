from script_trial import db


class AppInfo(db.Model):
    __tablename__ = 'app_deployment_info'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String())
    space_name = db.Column(db.String())
    version = db.Column(db.String())
    user_name = db.Column(db.String())
    deploy_time = db.Column(db.String())
    pr_info_id = db.Column(db.String())
    misc_info = db.Column(db.String())
    created_at = db.Column(db.String())



    def __init__(self, app_name, space_name, version, user_name, deploy_time, pr_info_id, misc_info, created_at):
        self.app_name = app_name
        self.space_name = space_name
        self.version = version
        self.user_name = user_name
        self.deploy_time = deploy_time
        self.pr_info_id = pr_info_id
        self.misc_info = misc_info
        self.created_at = created_at


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'app_name': self.app_name,
            'space_name': self.space_name,
            'version': self.version,
            'user_name': self.user_name,
            'deploy_time': self.deploy_time,
            'pr_info_id': self.pr_info_id,
            'misc_info': self.misc_info,
            'created_at': self.created_at
        }