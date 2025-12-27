import os
import pandas as pd
from fastapi import FastAPI, BackgroundTasks, HTTPException
from src.graph import create_nexus_graph
from src.llm_factory import get_llm
from src.prompts import CAMPAIGN_SUMMARY_PROMPT
import re

# 1. Initialize FastAPI
app = FastAPI(
    title="NexusAI: Agentic Sales CRM",
    description="An AI-powered system that autonomously processes leads, drafts emails, and simulates responses.",
    version="1.0.0"
)

# 2. Compile the LangGraph
nexus_graph = create_nexus_graph()

def run_campaign_logic():
    """
    Background task to process the full campaign pipeline.
    """
    try:
        # Step A: Ensure required directories exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("reports", exist_ok=True)

        # Step B: Load leads from CSV
        input_path = "data/lead.csv"
        if not os.path.exists(input_path):
            print(f"❌ Error: {input_path} not found. Please place your leads.csv in the data/ folder.")
            return

        print(f"📂 Loading leads from {input_path}...")
        df = pd.read_csv(input_path)
        
        results = []
        total_leads = len(df)
        print(f"🚀 Starting NexusAI Engine for {total_leads} leads.")

        # Step C: Loop through leads and invoke the Agentic Graph
        for index, row in df.iterrows():
            lead_email = row.get('Email', 'Unknown')
            print(f"--- 🤖 [{index+1}/{total_leads}] Processing: {lead_email} ---")
            
            # Prepare the initial state for the graph
            initial_state = {
                "lead_data": row.to_dict(),
                "priority": "",
                "priority_score": 0,
                "priority_reason": "",
                "persona": "",
                "persona_description": "",
                "email_subject": "",
                "email_body": "",
                "simulated_reply": "",
                "response_category": "",
                "status": "Pending"
            }
            
            # Execute the Graph (Scorer -> Enricher -> Drafter -> Sender -> Simulator -> Categorizer)
            try:
                final_state = nexus_graph.invoke(initial_state)
                results.append(final_state)
                print(f"✅ Finished processing {lead_email} | Category: {final_state.get('response_category')}")
            except Exception as node_err:
                print(f"⚠️ Error processing {lead_email}: {node_err}")
                initial_state["status"] = f"Failed: {str(node_err)}"
                results.append(initial_state)

        # Step D: Save the Enriched Data to CSV
        print("💾 Saving enriched results to data/enriched_leads.csv...")
        enriched_df = pd.DataFrame(results)
        
        # Flatten lead_data for a cleaner CSV output
        if not enriched_df.empty and 'lead_data' in enriched_df.columns:
            lead_details = pd.json_normalize(enriched_df['lead_data'])
            final_df = pd.concat([lead_details, enriched_df.drop(columns=['lead_data'])], axis=1)
            final_df.to_csv("data/enriched_leads.csv", index=False)
        else:
            enriched_df.to_csv("data/enriched_leads.csv", index=False)

        # Step E: Generate AI Campaign Summary Report
        print("📊 Generating Executive Campaign Summary...")
        llm = get_llm(temperature=0)
        
        # Pass the summary results to the LLM
        # We only pass key info to keep the prompt small and efficient
        summary_input = [
            {
                "email": r['lead_data'].get('Email'), 
                "priority": r.get('priority'), 
                "category": r.get('response_category')
            } for r in results
        ]
        
        report_response = llm.invoke([
            ("system", CAMPAIGN_SUMMARY_PROMPT),
            ("human", f"Summarize these campaign results:\n{str(summary_input)}")
        ])
        
        final_report_content = re.sub(r'<think>.*?</think>', '', report_response.content, flags=re.DOTALL).strip()
        # Save the Markdown report
        report_path = "reports/campaign_summary.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(final_report_content)
            
        print(f"🏁 Campaign Complete! Report available at {report_path}")

    except Exception as e:
        print(f"❌ CRITICAL ERROR IN BACKGROUND TASK: {e}")

@app.get("/")
async def root():
    return {"message": "NexusAI CRM is running. Use POST /run-campaign to start."}

@app.post("/run-campaign")
async def trigger_campaign(bt: BackgroundTasks):
    """
    Triggers the autonomous AI sales agent pipeline.
    """
    # Verify input file exists before starting
    if not os.path.exists("data/lead.csv"):
        raise HTTPException(status_code=404, detail="data/lead.csv not found.")
    
    bt.add_task(run_campaign_logic)
    return {
        "status": "Success",
        "message": "Campaign execution started in the background.",
        "instructions": "Check the 'reports/' folder for the summary and MailHog (localhost:8025) for emails."
    }

if __name__ == "__main__":
    import uvicorn
    # Create folders just in case before starting server
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)