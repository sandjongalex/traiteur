from flask import abort, redirect, render_template, request, url_for
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from ...extensions import db
from ...models.quote_request import QuoteRequest, QuoteRequestItem, QuoteRequestStatus
from . import quote_request_admin_bp
from ...services.rbac import permission_required
from ...services.audit import AuditService
from flask_login import current_user


@quote_request_admin_bp.get("/")
@permission_required("quote_request.view")
def request_list():
    status = request.args.get("status", "").strip().upper()
    search = request.args.get("q", "").strip()

    stmt = select(QuoteRequest).order_by(QuoteRequest.created_at.desc())
    if status:
        if status not in {item.value for item in QuoteRequestStatus}:
            abort(400)
        stmt = stmt.where(QuoteRequest.status == status)
    if search:
        stmt = stmt.where(
            or_(
                QuoteRequest.reference.contains(search),
                QuoteRequest.customer_name.contains(search),
            )
        )

    items = db.session.scalars(stmt.limit(200)).all()
    return render_template(
        "admin/quote_requests/list.html",
        items=items,
        statuses=list(QuoteRequestStatus),
        selected_status=status,
        search=search,
        title="Demandes de devis",
    )


@quote_request_admin_bp.get("/<int:item_id>")
@permission_required("quote_request.view")
def request_detail(item_id):
    item = db.session.scalar(
        select(QuoteRequest)
        .options(selectinload(QuoteRequest.items))
        .where(QuoteRequest.id == item_id)
    )
    if item is None:
        abort(404)
    return render_template(
        "admin/quote_requests/detail.html",
        item=item,
        statuses=list(QuoteRequestStatus),
        title=item.reference,
    )


@quote_request_admin_bp.post("/<int:item_id>/status")
@permission_required("quote_request.edit")
def update_status(item_id):
    item = db.get_or_404(QuoteRequest, item_id)
    new_status = request.form.get("status", "").strip().upper()
    allowed = {status.value for status in QuoteRequestStatus}
    if new_status not in allowed:
        abort(400)

    item.status = new_status
    AuditService.log("quote_request.status_change","QuoteRequest",item.id,f"Statut → {new_status}",user=current_user)
    db.session.commit()
    return redirect(url_for("quote_request_admin.request_detail", item_id=item.id))
