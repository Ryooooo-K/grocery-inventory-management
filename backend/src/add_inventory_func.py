import logging
import os

import azure.functions as func
from azure.cosmos import CosmosClient

from utils import get_cosmos_container_client

bp = func.Blueprint()


@bp.route(route="add_inventory", methods=["POST"])
async def add_inventory_item(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body: dict = req.get_json()
        item_name = req_body.get("item_name")
        quantity = req_body.get("quantity")

        if not item_name or not quantity:
            return func.HttpResponse(
                "Invalid request. 'item_name' and 'quantity' are required.",
                status_code=400,
            )

        container: CosmosClient = get_cosmos_container_client()
        item = {"id": item_name, "quantity": quantity}
        container.create_item(item)

        return func.HttpResponse(
            f"Item '{item_name}' with quantity {quantity} added successfully.",
            status_code=201,
        )
    except Exception as e:
        logging.error(f"Error adding inventory item: {e}")
        return func.HttpResponse(
            "An error occurred while adding the inventory item.",
            status_code=500,
        )
