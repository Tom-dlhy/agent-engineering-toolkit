# ant-design — component engineering and APIs

**Read when:** implementing Form, Table, Select, Modal, Upload, DatePicker or debugging a behavior/prop contract with ant-design. **Do not read** for unrelated CSS or another UI provider.

## Scope and compatibility

Use Ant Design when rich data-entry workflows dominate; take its form store, table and locale contracts seriously.

Project check: find package name/major version, framework runtime, SSR boundary, current import paths and installed examples first. Official API source: https://ant.design/components/overview/ . Prefer the project's installed contract if upstream docs target a newer major version.

## Provider-specific implementation knowledge

### Form state and validation
Ant Design's `Form` orchestrates values/validation through `Form.Item`; mixing React state with `initialValues` incorrectly can cause stale UI. For dynamic fields use Form.List and stable identifiers.
```tsx
import { Form, Input, Button } from 'antd'
type Values = { email: string }
export function Example() {
  const [form] = Form.useForm<Values>()
  return <Form form={form} onFinish={(data) => console.log(data.email)}>
    <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
      <Input autoComplete="email" />
    </Form.Item>
    <Button htmlType="submit">Save</Button>
  </Form>
}
```
Do not print personal form values in production logs; example console output is illustrative only. Use official event and field-naming contracts rather than HTML `onChange` assumptions.

## Component decision / execution playbook

1. **Choose component anatomy:** consult the exact package's current part/slot composition; make no substitution across primitive vendors.
2. **Model state:** document value, input/selected/open distinction; controlled vs uncontrolled; keyboard/disabled/error/loading; how async data changes state.
3. **Implement inside existing system:** reuse installed wrappers, tokens, typography, form validation and router, avoiding a new package where supported primitives suffice.
4. **Validate behavior:** test mouse, keyboard, screen reader, narrow screen, non-English strings and pending network state; record incorrect semantics and fix.
5. **Inspect negative paths:** empty/no-results, invalid selection, two quick submits, close while pending, focus after unmount and hydration.

## Anti-patterns

- Copying snippets across different major versions or framework bindings.
- Treating a visual state as adequate accessibility; missing keyboard/focus or label semantics.
- Mixing primitive systems and their slot conventions without reviewing refs/events.
- Changing the global theme merely to fix a single component; choose nearest coherent scope.

## Exit evidence

Identify inspected package version and source file, positive and negative tests run, unsupported scenarios and documentation source. Do not assert official API details from memory when the installed version is unknown.
