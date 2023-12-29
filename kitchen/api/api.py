import uuid
from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint

from api.schemas import (
    GetScheduleOrderSchema,
    ScheduleOrderSchema,
    GetScheduleOrdersSchema,
    ScheduleStatusSchema,
)

blueprint = Blueprint("kitchen", __name__, description="Kitchen API")

schedules = [{
    "id": str(uuid.uuid4()),
    "scheduled": datetime.now(),
    "status": "pending",
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "bog"
        }
    ]
}]


@blueprint.route("/kitchen/schedules")
class KitchenSchedules(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduleOrdersSchema)
    def get(self):
        return {"schedules": schedules}

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduleOrdersSchema)
    def post(self):
        return schedules[0]


@blueprint.route("/kitchen/schedules/<schedule_id>")
class KitchenSchedule(MethodView):
    @blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
    def get(self, schedule_id):
        return schedules[0]

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
    def post(self, schedule_id):
        return schedules[0]

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        return


@blueprint.response(status_code=200, schema=GetScheduleOrderSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/cancel", methods=["POST"])
def cancel_schedule(schedule_id):
    return schedules[0]


@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
@blueprint.route("/kitchen/schedules/<schedule_id>/status", methods=["POST"])
def get_schedule_status(schedule_id):
    return schedules[0]

