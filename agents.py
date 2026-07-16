class IntakeAgent:
    """
    Agent 1: Intake (Industry-Agnostic, White-Label)

    Collects customer/user info, classifies request type, and queries the Knowledge Base.
    This agent is customizable for any industry by injecting industry-specific prompts and
    escalation rules from the tenant_configs.

    Examples:
    - Agriculture (Mana Kai): Classify sensor anomalies, optimize watering
    - Plumbing: Classify emergency vs. routine service requests
    - Retail: Classify product questions, order status, returns
    - Healthcare: Collect patient info, triage by urgency
    """

    def __init__(
        self,
        knowledge_base_client,
        memory_store,
        tenant_id=None,
        tenant_config=None,
        db_session=None,
    ):
        self.kb_client = knowledge_base_client
        self.memory = memory_store
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.db_session = db_session  # TenantAwareDB instance

    def process_interaction(self, unified_message):
        """Main entry point from the Orchestrator."""
        print(
            f"Intake Agent: Processing incoming message ID "
            f"{unified_message.get('id')} for tenant {self.tenant_id}"
        )

        # 1. Extract and verify customer details
        customer_profile = self._collect_customer_info(unified_message)

        # 2. Classify the intent using tenant-specific rules
        request_classification = self._classify_request_type(unified_message)

        # 3. Update conversation state in Memory Store
        self.memory.update_context(
            unified_message.get("id"), customer_profile, request_classification
        )

        # 4. Query knowledge base for tenant-specific context
        if request_classification == "general_inquiry":
            return self._query_knowledge_base(unified_message.get("content"))
        else:
            # Pass back to Orchestrator to hand off to Fulfilment or Resolution
            return {
                "status": "handoff_required",
                "target_agent": self._determine_next_agent(
                    request_classification
                ),
                "context": customer_profile,
            }

    def _collect_customer_info(self, message):
        # Extract tenant-aware user/customer profile data from the normalized
        # payload
        return {
            "customer_id": message.get("customer_id"),
            "customer_name": message.get("customer_name"),
            "tenant_id": self.tenant_id,
        }

    def _classify_request_type(self, message):
        # Intent classification can be enriched with tenant-specific prompts and policies
        # Placeholder implementation; replace with actual LLM or rules engine.
        if "order" in message.get("content", "").lower():
            return "order_update"
        if "help" in message.get("content", "").lower():
            return "general_inquiry"
        return "general_inquiry"

    def _query_knowledge_base(self, query):
        # Perform a tenant-aware RAG lookup via the knowledge base client.
        if not self.tenant_id:
            raise ValueError(
                "Tenant ID is required for querying the knowledge base."
            )

        results = self.kb_client.query(query, tenant_id=self.tenant_id)
        prompt = self._build_rag_prompt(query, results)

        return {
            "status": "knowledge_response",
            "tenant_id": self.tenant_id,
            "query": query,
            "prompt": prompt,
            "results": results,
        }

    def _get_config_value(self, key, default=None):
        if isinstance(self.tenant_config, dict):
            return self.tenant_config.get(key, default)
        return getattr(self.tenant_config, key, default)

    def _build_rag_prompt(self, query, results):
        brand_voice = self._get_config_value(
            "brand_voice", "Helpful and concise."
        )
        custom_instructions = self._get_config_value("custom_instructions", "")

        knowledge_chunks = (
            "\n\n".join([f"- {item['content']}" for item in results])
            if results
            else "No relevant tenant knowledge was found."
        )

        return (
            f"You are a helpdesk assistant for tenant {self.tenant_id}.\n"
            f"Brand voice: {brand_voice}\n"
            f"{custom_instructions}\n\n"
            "Use the following tenant-specific knowledge to answer the customer query. "
            "Do not use any data from other tenants.\n\n"
            "Tenant knowledge:\n"
            f"{knowledge_chunks}\n\n"
            f"Customer question: {query}\n"
        )

    def _determine_next_agent(self, classification):
        # Simple routing logic
        if classification in ["order_update", "purchase", "booking"]:
            return "FulfillmentAgent"
        return "ResolutionAgent"


class FulfilmentAgent:
    """
    Agent 2: Fulfillment (Industry-Agnostic, White-Label)

    Executes tasks, processes business logic, and updates data records.
    This agent adapts to any industry by applying tenant-specific escalation rules and workflows.

    Examples:
    - Agriculture: Trigger watering systems, log growth metrics
    - Plumbing: Dispatch technician, generate invoice
    - Retail: Check inventory, process refund or upsell
    - Healthcare: Schedule appointment, verify insurance
    """

    def __init__(
        self,
        crm_client,
        order_db,
        llm_pool,
        tenant_id=None,
        escalation_rules=None,
        db_session=None,
    ):
        self.crm_client = crm_client
        self.order_db = order_db
        self.llm_pool = llm_pool
        self.tenant_id = tenant_id
        self.escalation_rules = escalation_rules or {}
        self.db_session = db_session  # TenantAwareDB instance

    def execute_task(self, task_context):
        """Main execution block triggered by the Orchestrator."""
        print(
            f"Fulfillment Agent: Executing task for customer "
            f"{task_context.get('customer_id')} on tenant {self.tenant_id}"
        )

        intent = task_context.get("intent")

        try:
            if intent == "process_order":
                result = self._process_new_order(task_context)
            elif intent == "update_record":
                result = self._update_customer_record(task_context)
            else:
                result = self._process_generic_task(task_context)

            return {
                "status": "success",
                "action_taken": result,
                "message_to_customer": "Your request has been processed successfully.",
            }

        except Exception as e:
            # If things go pear-shaped, prepare for handoff to Resolution
            return {
                "status": "failed",
                "error": str(e),
                "handoff_required": "ResolutionAgent",
            }

    def _process_new_order(self, context):
        # Industry-agnostic scaffold for order processing
        if not self.tenant_id:
            raise ValueError("Tenant ID is required for task execution.")
        return {"task": "process_order", "tenant_id": self.tenant_id}

    def _update_customer_record(self, context):
        # Industry-agnostic scaffold for updating CRM data
        if not self.tenant_id:
            raise ValueError("Tenant ID is required for task execution.")
        return {"task": "update_record", "tenant_id": self.tenant_id}

    def _process_generic_task(self, context):
        # Generic fallback, configured by tenant-specific workflow definitions
        if not self.tenant_id:
            raise ValueError("Tenant ID is required for task execution.")
        return {
            "task": "generic_task",
            "tenant_id": self.tenant_id,
            "intent": context.get("intent"),
        }


class ResolutionAgent:
    """
    Agent 3: Resolution (Industry-Agnostic, White-Label)

    Troubleshoots complex issues, logs telemetry, and manages escalations.
    This agent applies tenant-specific escalation criteria and compliance requirements.

    Examples:
    - Agriculture: Diagnose sensor failures or unusual growth patterns
    - Plumbing: Troubleshoot complex issues, escalate to senior technician
    - Retail: Resolve complaints, offer adjustments or escalate
    - Healthcare: Handle patient concerns, escalate to clinician
    """

    def __init__(
        self,
        telemetry_logger,
        escalation_queue,
        tenant_id=None,
        compliance_mode=None,
    ):
        self.logger = telemetry_logger
        self.escalation = escalation_queue
        self.tenant_id = tenant_id
        self.compliance_mode = compliance_mode or {}

    def handle_issue(self, issue_context):
        """Resolves edge cases or handles failed fulfilment tasks."""
        print(
            f"Resolution Agent: Troubleshooting issue "
            f"{issue_context.get('issue_id')}"
        )

        # Log the intervention for metrics
        self.logger.log_event("agent_intervention", issue_context)

        resolution_plan = self._generate_troubleshooting_steps(issue_context)

        if not resolution_plan.get("can_auto_resolve"):
            return self._escalate_to_human(issue_context)

        return self._apply_fix(resolution_plan)

    def _generate_troubleshooting_steps(self, context):
        # Scaffold for LLM diagnostic reasoning
        pass

    def _apply_fix(self, plan):
        # Scaffold for executing technical fixes
        pass

    def _escalate_to_human(self, context):
        # Scaffold for pushing to the Escalation Queue
        self.escalation.push(context)
        return {
            "status": "escalated",
            "message": "A human agent will be with you shortly.",
        }
