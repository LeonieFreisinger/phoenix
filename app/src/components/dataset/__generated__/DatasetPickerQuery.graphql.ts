/**
 * @generated SignedSource<<4f34f1e6015cd23ecf69f2f8126fe8d3>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type DatasetPickerQuery$variables = Record<PropertyKey, never>;
export type DatasetPickerQuery$data = {
  readonly datasets: {
    readonly edges: ReadonlyArray<{
      readonly dataset: {
        readonly exampleCount: number;
        readonly id: string;
        readonly name: string;
      };
    }>;
  };
};
export type DatasetPickerQuery = {
  response: DatasetPickerQuery$data;
  variables: DatasetPickerQuery$variables;
};

const node: ConcreteRequest = (function(){
var v0 = [
  {
    "alias": null,
    "args": null,
    "concreteType": "DatasetEdge",
    "kind": "LinkedField",
    "name": "edges",
    "plural": true,
    "selections": [
      {
        "alias": "dataset",
        "args": null,
        "concreteType": "Dataset",
        "kind": "LinkedField",
        "name": "node",
        "plural": false,
        "selections": [
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "id",
            "storageKey": null
          },
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "name",
            "storageKey": null
          },
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "exampleCount",
            "storageKey": null
          }
        ],
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "cursor",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "concreteType": "Dataset",
        "kind": "LinkedField",
        "name": "node",
        "plural": false,
        "selections": [
          {
            "alias": null,
            "args": null,
            "kind": "ScalarField",
            "name": "__typename",
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ],
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "concreteType": "PageInfo",
    "kind": "LinkedField",
    "name": "pageInfo",
    "plural": false,
    "selections": [
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "endCursor",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "hasNextPage",
        "storageKey": null
      }
    ],
    "storageKey": null
  }
],
v1 = [
  {
    "kind": "Literal",
    "name": "first",
    "value": 100
  }
];
return {
  "fragment": {
    "argumentDefinitions": [],
    "kind": "Fragment",
    "metadata": null,
    "name": "DatasetPickerQuery",
    "selections": [
      {
        "alias": "datasets",
        "args": null,
        "concreteType": "DatasetConnection",
        "kind": "LinkedField",
        "name": "__DatasetPicker__datasets_connection",
        "plural": false,
        "selections": (v0/*: any*/),
        "storageKey": null
      }
    ],
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [],
    "kind": "Operation",
    "name": "DatasetPickerQuery",
    "selections": [
      {
        "alias": null,
        "args": (v1/*: any*/),
        "concreteType": "DatasetConnection",
        "kind": "LinkedField",
        "name": "datasets",
        "plural": false,
        "selections": (v0/*: any*/),
        "storageKey": "datasets(first:100)"
      },
      {
        "alias": null,
        "args": (v1/*: any*/),
        "filters": null,
        "handle": "connection",
        "key": "DatasetPicker__datasets",
        "kind": "LinkedHandle",
        "name": "datasets"
      }
    ]
  },
  "params": {
    "cacheID": "ba71791351337fdd4016ab2dc41ef65e",
    "id": null,
    "metadata": {
      "connection": [
        {
          "count": null,
          "cursor": null,
          "direction": "forward",
          "path": [
            "datasets"
          ]
        }
      ]
    },
    "name": "DatasetPickerQuery",
    "operationKind": "query",
    "text": "query DatasetPickerQuery {\n  datasets(first: 100) {\n    edges {\n      dataset: node {\n        id\n        name\n        exampleCount\n      }\n      cursor\n      node {\n        __typename\n      }\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n"
  }
};
})();

(node as any).hash = "5949a605c226a9ac97df28e12c7858bd";

export default node;
