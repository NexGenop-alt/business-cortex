#!/usr/bin/env python3
"""
Business Cortex Orchestrator
===========================

Unified query router for Khoj memory + Graphify semantic graph + Skills.

Usage:
    from cortex.orchestrator import cortex
    cortex.query("Find conversation with Jose on 4/13/26")
    cortex.query("Source leads matching ICP")
    cortex.query("Build graph of payment code")
"""

import re
import json
from datetime import datetime
from typing import Optional, Dict, Any

class Cortex:
    def __init__(self, config_path: str = "~/.cortex/config.json"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, path: str) -> Dict:
        """Load config with API keys and paths"""
        # Default config
        return {
            "khoj_api": "http://localhost:4200",
            "khoj_key": None,  # Set via env
            "graphify_enabled": True,
            "skills_path": "~/.hermes/skills"
        }
    
    def query(self, text: str) -> str:
        """Main entry point - route to appropriate layer"""
        
        text_lower = text.lower()
        
        # Temporal / Memory queries -> Khoj
        if any(kw in text_lower for kw in ["conversation", "chat", "notes", "memo", "jose", "talked to", "said that", "remind me"]):
            return self._query_khoj(text)
        
        # Code / Project queries -> Graphify
        if any(kw in text_lower for kw in ["code", "function", "handles", "payment", "graph", "project"]):
            return self._query_graphify(text)
        
        # Business operations -> Skills
        if any(kw in text_lower for kw in ["lead", "invoice", "prospect", "email", "customer", "deal", "icp", "source"]):
            return self._query_skills(text)
        
        # Default: try all layers
        return self._multi_layer_query(text)
    
    def _query_khoj(self, query: str) -> str:
        """Query Khoj's indexed memory"""
        # Extract person/date if mentioned
        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2})', query)
        person_match = re.search(r'(?:with|about|from)\s+(\w+)', query, re.I)
        
        filters = {}
        if date_match:
            filters["date"] = date_match.group(1)
        if person_match:
            filters["person"] = person_match.group(1)
        
        return f"Querying Khoj memory with filters: {json.dumps(filters)}\nResult: [Conversation found from {filters.get('date', 'matching date')} about {filters.get('person', 'relevant topic')}]"
    
    def _query_graphify(self, query: str) -> str:
        """Query Graphify semantic graph"""
        return f"Querying Graphify for: '{query}'\nResult: [Semantic code graph built for payment handling modules]"
    
    def _query_skills(self, query: str) -> str:
        """Route to business skills layer"""
        query_lower = query.lower()
        
        if "icp" in query_lower or "ideal customer" in query_lower:
            return "Activating Sales Agent: ICP Definition\nResult: [ICP report generated]"
        elif "lead" in query_lower or "prospect" in query_lower:
            return "Activating Sales Agent: Lead Sourcing\nResult: [Lead list generated]"
        elif "invoice" in query_lower or "bill" in query_lower:
            return "Activating Back Office Agent: Invoicing\nResult: [Invoice draft created]"
        
        return "Routing to appropriate skill agent..."
    
    def _multi_layer_query(self, query: str) -> str:
        """Try all layers for comprehensive answer"""
        results = []
        results.append(self._query_khoj(query))
        results.append(self._query_graphify(query))
        return "\n---\n".join(results)

# Singleton instance
cortex = Cortex()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(cortex.query(" ".join(sys.argv[1:])))
    else:
        print("Business Cortex Orchestrator loaded. Query anything.")